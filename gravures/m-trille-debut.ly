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
      \key c \major c''4\prall_\markup \small \italic "mordant sup." c''4\trill_\markup \small \italic "trille" d''4\trill d''4-\tweak self-alignment-X #CENTER ^\markup \override #'(baseline-skip . 1.9) \center-column { \teeny \flat \musicglyph "scripts.trill" }
      \bar "|."
    }
    \new Staff \with { instrumentName = \markup \small \italic "joué" } {
      \clef treble \time 4/4 \autoBeamOff
      \key c \major c''32[ d''32_\markup \tiny \italic "ton" c''8.] c''32[ d''32_\markup \tiny \italic "ton" c''32 d''32 c''32 d''32 c''16] d''32[ e''32_\markup \tiny \italic "ton" d''32 e''32 d''32 e''32 d''16] d''32[ ees''32_\markup \tiny \italic "demi-ton" d''32 ees''32 d''32 ees''32 d''16]
      \bar "|."
    }
  >>
  \layout {
    indent = 17\mm
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 }
  }
}
