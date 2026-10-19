\version "2.24.3"
%% Fichier produit par outils/generer_ornements.py — ne pas modifier à la main.
\paper {
  indent = 0
  ragged-right = ##t
  top-margin = 1\mm
  bottom-margin = 1\mm
  left-margin = 1\mm
  right-margin = 1\mm
  oddHeaderMarkup = ##f
  evenHeaderMarkup = ##f
  oddFooterMarkup = ##f
  evenFooterMarkup = ##f
  bookTitleMarkup = ##f
  scoreTitleMarkup = ##f
}
\score {
  \new StaffGroup <<
    \new Staff \with { instrumentName = \markup \small \italic "écrit" } {
      \clef treble \time 4/4
      \key c \major e''2 \grace { f''16[ g'' a'' g'' f'' e'' d'' e''] } f''2
      \bar "|."
    }
    \new Staff \with { instrumentName = \markup \small \italic "joué" } {
      \clef treble \time 4/4 \autoBeamOff
      \key c \major e''4 f''32[ g''32 a''32 g''32 f''32 e''32 d''32 e''32] f''2
      \bar "|."
    }
  >>
  \layout {
    indent = 17\mm
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 }
  }
}
