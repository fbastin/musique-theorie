\version "2.24.3"
%% Fichier produit par outils/generer_mordants.py — ne pas modifier à la main.
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
      \key c \major c''4\mordent d''4\mordent e''4\mordent f''4\mordent
      \bar "|."
    }
    \new Staff \with { instrumentName = \markup \small \italic "joué" } {
      \clef treble \time 4/4 \autoBeamOff
      \key c \major c''32[ b'32_\markup \tiny \italic "demi-ton" c''8.] d''32[ c''32_\markup \tiny \italic "ton" d''8.] e''32[ d''32_\markup \tiny \italic "ton" e''8.] f''32[ e''32_\markup \tiny \italic "demi-ton" f''8.]
      \bar "|."
    }
  >>
  \layout {
    indent = 17\mm
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 }
  }
}
